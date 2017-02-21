/* Javascript for CodePlayground XBlock (student_view). */
function CodePlayground(runtime, xblock_element) {

  function handleSubmissionResults(results) {
    $(xblock_element).find('.problem-progress').html(results['points_earned'] + ' / ' + results['points_possible'] + ' points');
  }

  $(xblock_element).find('.input-main').bind('click', function() {
    var data = {
      "submitted_code": $(xblock_element).find('textarea[name=codeEditor]').val()
    };
    
    // call the Python JSON handler (code_submit) and process returned value
    var handlerUrl = runtime.handlerUrl(xblock_element, 'code_submit');
    $.post(handlerUrl, JSON.stringify(data)).success(handleSubmissionResults);
    
  });
}
