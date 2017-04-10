$(function() {

    var bar = $('.progress-bar');
    var percent = $('.percent');
    var status = $('#status');

    $('form').ajaxForm({
        beforeSend: function() {
            status.empty();
            var percentVal = '0%';
            bar.attr('aria-valuenow', percentVal).css('width', percentVal);
        },
        uploadProgress: function(event, position, total, percentComplete) {
            var percentVal = percentComplete + '%';
            bar.attr('aria-valuenow', percentVal).css('width', percentVal);
        },
        complete: function(xhr) {
            status.html(xhr.responseText);
        }
    });
});

$(document).ready(
    function(){
        $('input:file').change(
            function(){
                if ($(this).val()) {
                    $('#uploadButon').removeClass('disabled');
                    $('input:submit').attr('disabled',false);
                    $('.progress-bar').attr('aria-valuenow', '0%').css('width', '0%');
                    // or, as has been pointed out elsewhere:
                    // $('input:submit').removeAttr('disabled');
                }
            }
            );
});
