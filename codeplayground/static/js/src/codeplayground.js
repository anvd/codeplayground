/* Javascript for CodePlayground XBlock (student_view). */
function CodePlayground(runtime, xblock_element) {

	function handleSubmissionResult(results) {
		var errorMessage = results['error'];
		if (errorMessage != null) {
			$('xblock_element').find('div[name=errorMessageSession]').show();
			$('xblock_element').find('label[name=errorMessage]').val(errorMessage)
			return;
		} else {
			$('xblock_element').find('div[name=errorMessageSession]').hide();
		}
	
    	$(xblock_element).find('.problem-progress').html(results['points_earned'] + ' / ' + results['points_possible'] + ' points');
  	}
  	
  	function handleShowAnswerResult(results) {
  		var show_answer_button_text = results['show_answer_button_text'];
  		$(xblock_element).find('input[name=showanswer-button]').val(show_answer_button_text); 
  		
  		debugger;
  		if (show_answer_button_text == 'Show Answer') {
  			$(xblock_element).find('pre[name=answer]').html('');
  			$(xblock_element).find('div[name=codeSection]').hide();
  		} else {
  			$(xblock_element).find('pre[name=answer]').html(results['answer']);
  			$(xblock_element).find('div[name=codeSection]').show();
  		}
  	}

  	$(xblock_element).find('input[name=submit-button]').bind('click', function() {
    	var data = {
      		"submitted_code": $(xblock_element).find('textarea[name=codeEditor]').val()
    	};
    
    	var handlerUrl = runtime.handlerUrl(xblock_element, 'code_submit');
    	$.post(handlerUrl, JSON.stringify(data)).success(handleSubmissionResult);
  	});
  	
  	$(xblock_element).find('input[name=showanswer-button]').bind('click', function() {
  		var data = {
  			"previous_show_answer_button_text": $(xblock_element).find('input[name=showanswer-button]').val()
  		}
  		
  		var handlerUrl = runtime.handlerUrl(xblock_element, 'showanswer_clicked');
  		$.post(handlerUrl, JSON.stringify(data)).success(handleShowAnswerResult);
  	});
  	
  	
}
