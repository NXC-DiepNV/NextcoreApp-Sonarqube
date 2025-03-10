$(document).ready(function() {

    /**
     * Hidden all field input
     */
    function initForm() {
        $('.form-row.field-event').addClass('hidden')
        $('.form-row.field-gift').addClass('hidden')
        $('.form-row.field-from_user').addClass('hidden')
        $('.form-row.field-to_user').addClass('hidden')
        $('.form-row.field-fee').addClass('hidden')
    }
    
    /**
     * Handle change event type
     */
    $('#id_type').change(function() {
        initForm();
        $user_type = $('#id_user_type').val()
        console.log($user_type)
        const eventType = $(this).val();
        switch (eventType) {
            case 'increase':
            case 'decrease':
                updateEventOptions(eventType);
                $('.form-row.field-event').removeClass('hidden')
                if ($user_type != 'coin_user'){
                    $('.form-row.field-to_user').removeClass('hidden')
                }
                break
            case 'transfer':
                $('.form-row.field-from_user').removeClass('hidden')
                $('.form-row.field-to_user').removeClass('hidden')
                $('.form-row.field-fee').removeClass('hidden')
                break;
            case 'deposit':
            case 'withdraw':
                $('.form-row.field-to_user').removeClass('hidden')
                break;
            case 'exchange':
                $('.form-row.field-gift').removeClass('hidden')
                break;
            default:
                break
        }
    });

    // Call initForm function with value is 'increase' (default value)
    if ($('#id_type').val() === '') {
        $('#id_type').val('increase').change();
    } else {
        $('#id_type').val($('#id_type').val()).change();
    }

    /**
     * Filter event when select type
     */
    function updateEventOptions(selectedEventType) {
        $('#id_event').find('option').each(function() {
            const eventOption = $(this);
            const eventType = eventOption.data('type-id'); 

            if (eventType == selectedEventType) {
                eventOption.show();
            } else {
                eventOption.hide();
            }
        });

        if ($('#id_event').find('option:selected').is(':hidden')) {
            $('#id_event').val('');
        }
    }

});
