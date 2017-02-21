import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, String, Integer
from xblock.fragment import Fragment

from submissions import api as sub_api
from sub_api_util import SubmittingXBlockMixin


class CodePlaygroundXBlock(XBlock, SubmittingXBlockMixin):
    """
    An XBlock for teachers to write coding assignments and learners to practice coding.
    """

    # Settings
    display_name = String(display_name="Title (Display name)", help="Title to display", default="Code playground", scope=Scope.settings)

    attempts = Integer(display_name="Attempts",
        help="Number of attempts taken by the student on this problem",
        default=0,
        scope=Scope.user_state)
    max_attempts = Integer(
        display_name="Maximum Attempts",
        help="Defines the number of times a student can try to answer this problem. If the value is not set, infinite attempts are allowed.",
        values={"min": 0}, scope=Scope.settings)
    
    max_points = Integer(
        display_name="Possible points",
        help="Defines the maximum points that the learner can earn.",
        default=1,
        scope=Scope.settings)
    # gherkin_file = String(display_name="Gherkin file", help="BDD feature file name", default="", scope=Scope.settings)
    

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    question_content = String("Enter question content?", default="Enter the question...", scope=Scope.content)
    code_skeleton = String("Enter code here ...", default="Enter code...", scope=Scope.content)
    expected_output = String("Expected output ...", default="Enter expected output...", scope=Scope.content)
    
    # editable_fields = ('display_name', 'question') TODO use StudioEditableXBlockMixin to generate the form
    
    has_score = True

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the CodePlayground XBlock, shown to students when viewing courses.
        """
        # TODO render points
        
        html = self.resource_string("static/html/codeplayground.html")
        frag = Fragment(html.format(self=self))
        frag.add_javascript(self.resource_string("static/js/src/codeplayground.js"))
        frag.initialize_js('CodePlayground')

        return frag

    def studio_view(self, context=None):
        """
        The view of CodePlayground XBlock, shown to course author when clicking 'Edit' button in Studio
        """
        html = self.resource_string("static/html/codeplayground_edit.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/codeplayground.css"))
        frag.add_javascript(self.resource_string("static/js/src/codeplayground_edit.js"))
        frag.initialize_js('CodePlaygroundEdit')
        return frag        

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Course author pressed the Save button in Studio
        """

        result = {"submitted": "false", "saved": "false", "message": "", "preview": ""}

        if len(data) > 0:

            # Used for the preview feature
            # if data["commit"] == "true":
            
            self.display_name = data["display_name"]
            self.question_content = data["question_content"]
            self.code_skeleton = data["code_skeleton"]
            self.expected_output = data["expected_output"]
            self.max_points = data["max_points"]
            # self.gherkin_file = data["gherkin_file"]

            result["submitted"] = "true"
            result["saved"] = "true"

        return result
    
    @XBlock.json_handler
    def code_submit(self, data, suffix=''):
        """
        Learner pressed submit button to submit code
        """
        # TODO query feature file to run the testsuite
        # For the moment, if feature file is specified then returns 1 else 0

        submission = sub_api.create_submission(self.student_item_key, data)
        # sub_api.set_score(submission['uuid'], 1, 1) max_points.
        sub_api.set_score(submission['uuid'], 1, self.max_points)
        new_score = sub_api.get_score(self.student_item_key)

        return {
            'points_earned': new_score['points_earned'],
            'points_possible': new_score['points_possible']
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
            
