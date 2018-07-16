$(
function () {
    $(document).on('click', '.js_action', function(){
        var $this = $(this);
        var action = $this.data('action');
        var modal = $("#"+action);
        modal.parents('form').data('extradata', $this.data('extradata'));
        modal.parents('form').data('extracallback', function() {
            if ($this.data('deleterow')) {
                $this.parents('tr').remove();
            }
        });
        modal.modal('show');
    });
}
);