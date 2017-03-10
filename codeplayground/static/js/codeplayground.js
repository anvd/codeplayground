/* Javascript for CodePlayground XBlock (student_view). */
function CodePlayground(runtime, xblock_element) {

	function handleSubmissionResult(results) {
	
		debugger;
		var errorMessage = results['error'];
		var errorSectionElement = $(xblock_element).find('div[name=errorSection]');
		
		errorSectionElement.empty();
		if (errorMessage != null) {
			
			var errorLabelNode = "<label class='submit-error'>" + errorMessage + "</label>";
			errorSectionElement.append(errorLabelNode);
		}
	
    	$(xblock_element).find('.problem-progress').html(results['points_earned'] + ' / ' + results['points_possible'] + ' points');
  	}
  	
  	
  	function handleShowAnswerResult(results) {
  		var codeSectionElement = $(xblock_element).find('div[name=codeSection]');
  	
  		var answer_button_text = results['answer_button_text'];
  		$(xblock_element).find('input[name=showanswer-button]').val(answer_button_text); 
  		
  		if (answer_button_text == 'Show Answer') {
  			codeSectionElement.empty();
  		} else {
  			// TODO use template to avoid the maintenance nightmare
  			var labelNode = "<label><strong>Answer:</strong></label>";
  			codeSectionElement.append(labelNode);
  			
  			var preNode = "<pre name=\"answer\"><code>" + results['answer'] + "</code></pre>";
  			codeSectionElement.append(preNode);
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
  			"previous_answer_button_text": $(xblock_element).find('input[name=showanswer-button]').val()
  		}
  		
  		var handlerUrl = runtime.handlerUrl(xblock_element, 'showanswer_clicked');
  		$.post(handlerUrl, JSON.stringify(data)).success(handleShowAnswerResult);
  	});
  	
  	
}
