$(function() {
    $('select[name="monde"]').change(function() {
        $(this).parents('form').submit();
    });
});
