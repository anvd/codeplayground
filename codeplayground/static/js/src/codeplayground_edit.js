/* Javascript for CodePlayground XBlock (LMS and Studio edit). */
function CodePlaygroundEdit(runtime, element) {
  $(element).find('.save-button').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
    var data = {
      "display_name": $(element).find('input[name=displayName]').val(),
      "question_content": $(element).find('input[name=question]').val(),
      "code_skeleton": $(element).find('textarea[name=codeEditor]').val(),
      "expected_output": $(element).find('textarea[name=expectedOutput]').val(),
      "max_points": $(element).find('input[name=maximumPoint]').val()
    };
    runtime.notify('save', {state: 'start'});
    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
      runtime.notify('save', {state: 'end'});
    });
  });

  $(element).find('.cancel-button').bind('click', function() {
    runtime.notify('cancel', {});
  });
}
