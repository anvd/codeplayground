import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, String, Integer, Boolean
from xblock.fragment import Fragment

from submissions import api as sub_api
from sub_api_util import SubmittingXBlockMixin

from xblockutils.studio_editable import StudioEditableXBlockMixin
from xblockutils.resources import ResourceLoader

from utils import load_resource

loader = ResourceLoader(__name__)

@XBlock.needs("i18n")
class CodePlaygroundXBlock(XBlock, SubmittingXBlockMixin, StudioEditableXBlockMixin):
    """
    An XBlock for teachers to write coding assignments and learners to practice coding.
    """

    # Settings
    display_name = String(display_name="Title (Display name)", help="Title to display", default="Code playground", scope=Scope.settings)

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
    
    SHOW_ANSWER_BUTTON_SHOW_TEXT = "Show Answer"
    SHOW_ANSWER_BUTTON_HIDE_TEXT = "Hide Answer"

    showanswer = Boolean(
        display_name=SHOW_ANSWER_BUTTON_SHOW_TEXT,
        help="Defines when to show the answer",
        scope=Scope.settings,
        default=False
    )
    
    computed_answer_button_text = String(scope=Scope.user_state, default=SHOW_ANSWER_BUTTON_SHOW_TEXT) 
    
    answer = String(display_name="Answer", help="Enters the answer to show to learner", default="", multiline_editor=True, scope=Scope.settings)
    
    question_content = String(display_name="Enter question content", help="Enter the question", default="question content ...", multiline_editor=True, scope=Scope.content)
    code_skeleton = String(display_name="Code skeleton", help="Enter the code", default="Code skeleton...", multiline_editor=True, scope=Scope.content)
    expected_output = String(display_name="Expected output", help="Enter expected output", default="Expected output...", multiline_editor=True, scope=Scope.content)
    
    # For StudioEditableXBlockMixin to create the "edit" form
    editable_fields = ('display_name', 'max_attempts', 'max_points', 'question_content', 'code_skeleton', 'expected_output', 'showanswer', 'answer', 'grader_id')
    
    has_score = True


    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")


    def student_view(self, context=None):
        """
        The primary view of the CodePlayground XBlock, shown to students when viewing courses.
        """
        
        if not(self.showanswer):
            self.computed_answer_button_text = self.SHOW_ANSWER_BUTTON_SHOW_TEXT

        context = { 
            'point_string': self.point_string,
            'question_content': self.question_content,
            'showanswer': self.showanswer,
            'code_skeleton': self.code_skeleton,
            'expected_output': self.expected_output,
            'answer': '' if (self.computed_answer_button_text == self.SHOW_ANSWER_BUTTON_SHOW_TEXT) else self.answer,
            'answer_button_text': self.computed_answer_button_text
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
        # TODO query feature file to run the testsuite
        # For the moment, if feature file is specified then returns 1 else 0
        
        if (self.grader_id == ''):
            return {
                'error': 'You can not submit the assignment as no grader_id is configured'
            }

        submission = sub_api.create_submission(self.student_item_key, data)
        # sub_api.set_score(submission['uuid'], 1, 1) max_points.
        sub_api.set_score(submission['uuid'], 1, self.max_points)
        new_score = sub_api.get_score(self.student_item_key)

        return {
            'points_earned': new_score['points_earned'],
            'points_possible': new_score['points_possible']
        }
        
        
    @XBlock.json_handler
    def showanswer_clicked(self, data, suffix=''):
        """
        AJAX handler for "Show/Hide Answer" button
        """
        previous_show_answer_button_text = data['previous_show_answer_button_text']
        
        if (previous_show_answer_button_text == self.SHOW_ANSWER_BUTTON_SHOW_TEXT):
            self.computed_answer_button_text = self.SHOW_ANSWER_BUTTON_HIDE_TEXT
        else:
            self.computed_answer_button_text = self.SHOW_ANSWER_BUTTON_SHOW_TEXT
            
        return {
            'answer': self.answer,
            'show_answer_button_text': self.computed_answer_button_text
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
            
