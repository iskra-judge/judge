$(function () {
    function submitForm(ev) {
        const formData = new FormData(this);
        const method = $(this).attr('method');
        const url = $(this).attr('action');

        const data = {
            'task_id': formData.get('task_id'),
            'submission_type_id': formData.get('submission_type_id'),
            'code': formData.get('code'),
        };

        loading.show();
        http.post(url, data)
            .then(json => console.log(json))
            .catch(err => console.error(err))
            .finally(() => loading.hide());

        ev.preventDefault();
        return false;
    }

    $('.ajax-form').on('submit', submitForm);
});