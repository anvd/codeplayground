import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, String, Integer, Boolean, List
from xblock.fragment import Fragment

from submissions import api as sub_api
from sub_api_util import SubmittingXBlockMixin

from xblockutils.studio_editable import StudioEditableXBlockMixin
from xblockutils.resources import ResourceLoader

from utils import load_resource
import java_code_grader 

loader = ResourceLoader(__name__)


def language_provider():
    return [ 'Java', 'Python' ]


def assigment_provider():
    return [ 'MultiplyANumberByTwoGrader', 'MultiplyTwoNumbersGrader' ]


@XBlock.needs("i18n")
class CodePlaygroundXBlock(XBlock, SubmittingXBlockMixin, StudioEditableXBlockMixin):
    """
    An XBlock for teachers to write coding assignments and learners to practice coding.
    """

    # Settings
    display_name = String(
        display_name="Title (Display name)", 
        help="Title to display", 
        default="Code Playground", 
        scope=Scope.settings)

    languages = String(
        display_name="Programming language",
        help="Select the programming language",
        values=language_provider,
        default='Java',
        scope=Scope.settings
    )
    
    assignments = String(
        display_name="Assignment",
        help="Select the assignment",
        values=assigment_provider,
        default='MultiplyANumberByTwoGrader',
        scope=Scope.settings
    )
    
    max_attempts = Integer(
        display_name="Maximum Attempts",
        help="Defines the number of times a student can try to answer this problem. If the value is not set, infinite attempts are allowed.",
        values={"min": 0}, scope=Scope.settings)
    
    max_points = Integer(
        display_name="Possible points",
        help="Defines the maximum points that the learner can earn.",
        default=1,
        scope=Scope.settings)
    
    grader_id = String(display_name="Grader Id", help="Grader identifier", default="", scope=Scope.settings)
    # gherkin_file = String(display_name="Gherkin file", help="BDD feature file name", default="", scope=Scope.settings)
    
    SHOW_ANSWER_BUTTON_TEXT = "Show Answer"
    HIDE_ANSWER_BUTTON_TEXT = "Hide Answer"

    showanswer = Boolean(
        display_name=SHOW_ANSWER_BUTTON_TEXT,
        help="Defines when to show the 'Show/Hide Answer' button",
        default=False,
        scope=Scope.settings
    )
    
    answer_button_text = String(scope=Scope.user_state, default=SHOW_ANSWER_BUTTON_TEXT) 
    
    answer = String(
        display_name="Answer", 
        help="Enters the answer to show to learner", 
        default="", multiline_editor=True, 
        scope=Scope.settings)
    
    question_content = String(
        display_name="Enter question content", 
        help="Enter the question", 
        default="Please enter question content ...", 
        multiline_editor=True, 
        scope=Scope.content)
    
    code_skeleton = String(
        display_name="Code skeleton", 
        help="Enter the code", 
        default="Please enter code skeleton...", 
        multiline_editor=True, 
        scope=Scope.content)
    
    expected_output = String(
        display_name="Expected output", 
        help="Enter expected output", 
        default="Please enter the expected output...", 
        multiline_editor=True, 
        scope=Scope.content)
    
    # For StudioEditableXBlockMixin to create the "edit" form
    editable_fields = ('display_name', 'languages', 'assignments' ,'max_attempts', 'max_points', 'question_content', 'code_skeleton', 'expected_output', 'showanswer', 'answer', 'grader_id')
    
    has_score = True


    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")


    def studio_view(self, context):
        """
        Render a form for editing this XBlock (override the StudioEditableXBlockMixin's method)
        """
        fragment = Fragment()
        context = {'fields': []}
        # Build a list of all the fields that can be edited:
        for field_name in self.editable_fields:
            field = self.fields[field_name]
            assert field.scope in (Scope.content, Scope.settings), (
                "Only Scope.content or Scope.settings fields can be used with "
                "StudioEditableXBlockMixin. Other scopes are for user-specific data and are "
                "not generally created/configured by content authors in Studio."
            )
            field_info = self._make_field_info(field_name, field)
            if field_info is not None:
                context["fields"].append(field_info)
        fragment.content = loader.render_template('static/html/code_playground_studio_edit.html', context)
        # fragment.add_javascript(loader.load_unicode('public/studio_edit.js'))
        fragment.add_javascript(loader.load_unicode('static/js/src/codeplayground_studio_edit.js'))
        fragment.initialize_js('StudioEditableXBlockMixin')
        return fragment
    


    def student_view(self, context=None):
        """
        The primary view of the CodePlayground XBlock, shown to students when viewing courses.
        """
        
        if not(self.showanswer):
            self.answer_button_text = self.SHOW_ANSWER_BUTTON_TEXT

        context = { 
            'point_string': self.point_string,
            'question_content': self.question_content,
            'showanswer': self.showanswer,
            'code_skeleton': self.code_skeleton,
            'expected_output': self.expected_output,
            'answer': '' if (self.answer_button_text == self.SHOW_ANSWER_BUTTON_TEXT) else self.answer,
            'answer_button_text': self.answer_button_text
        }
        
        
        frag = Fragment()
        
        frag.content = loader.render_template('static/html/codeplayground.html', context)
        frag.add_css(self.resource_string("static/css/codeplayground.css"))
        frag.add_javascript(self.resource_string("static/js/src/codeplayground.js"))
        frag.initialize_js('CodePlayground')

        return frag


    @XBlock.json_handler
    def code_submit(self, data, suffix=''):
        """
        AJAX handler for Submit button
        """
        
        if (self.grader_id == ''):
            return {
                'error': 'You can not submit the assignment as no grader_id is configured'
            }

        submission = sub_api.create_submission(self.student_item_key, data)

        submitted_code = data["submitted_code"]
        grading_result = java_code_grader.grade(self.grader_id, submitted_code)
        if grading_result.has_key("error"):
            sub_api.set_score(submission['uuid'], 0, self.max_points)
        else:
            sub_api.set_score(submission['uuid'], self.max_points, self.max_points)
        
        new_score = sub_api.get_score(self.student_item_key)
        
        submit_result = {
            'points_earned': new_score['points_earned'],
            'points_possible': new_score['points_possible']
        }
        
        if grading_result.has_key("error"):
            submit_result["error"] = grading_result["error"]
            
        return submit_result
        
        
    @XBlock.json_handler
    def showanswer_clicked(self, data, suffix=''):
        """
        AJAX handler for "Show/Hide Answer" button
        """
        previous_answer_button_text = data['previous_answer_button_text']
        
        if (previous_answer_button_text == self.SHOW_ANSWER_BUTTON_TEXT):
            self.answer_button_text = self.HIDE_ANSWER_BUTTON_TEXT
        else:
            self.answer_button_text = self.SHOW_ANSWER_BUTTON_TEXT
            
        return {
            'answer': self.answer,
            'answer_button_text': self.answer_button_text
        }

    
    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("CodePlayground",
             """<codeplayground/>
             """),
            ("Multiple CodePlayground",
             """<vertical_demo>
                <codeplayground/>
                <codeplayground/>
                <codeplayground/>
                </vertical_demo>
             """),
        ]
        
    @property
    def point_string(self):
        score = sub_api.get_score(self.student_item_key)
        
        if score != None:
            return str(score['points_earned']) + ' / ' + str(score['points_possible']) + ' point(s)'
        else:
            return str(self.max_points) + ' point(s) possible'
            


