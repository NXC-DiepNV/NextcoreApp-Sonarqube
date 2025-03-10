(function ($) {
    'use strict';

    $(document).ready(function () {
        $(".formatted-number").on("keypress", function (e) {
            if (e.which < 48 || e.which > 57) {
                e.preventDefault();
            }
        });
    
        $(".formatted-number").on("input", function () {
            let cursorPosition = this.selectionStart;
            let value = $(this).val().replace(/[^0-9]/g, ""); 
    
            if (value !== "") {
                $(this).val(Number(value).toLocaleString("en-US"));
            } else {
                $(this).val("");
            }
    
            let lengthDiff = $(this).val().length - value.length;
            this.setSelectionRange(cursorPosition + lengthDiff, cursorPosition + lengthDiff);
        });
    });
    
})(jQuery);
