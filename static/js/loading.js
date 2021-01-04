(function(scope) {
    const $loading = $('.loading');

    function showHide() {
        $loading.toggleClass('loading-hidden');
    }

    scope.loading = {
        show: showHide,
        hide: showHide,
    };
}(window))