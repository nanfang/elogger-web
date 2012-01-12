angular.directive('my:fancybox', function(expression, compiledElement) {
    var compiler = this;
    return function(linkElement) {
        var currentScope = this;
        var log = currentScope.log;
        $(linkElement).fancybox({
                title: "修改记录",
                maxWidth    : 800,
                maxHeight    : 600,
                fitToView    : false,
                width        : '70%',
                height        : '70%',
                autoSize    : false,
                closeClick    : false,
                openEffect    : 'none',
                closeEffect    : 'none',
                beforeLoad: function() {
                    this.title = log.title;
                },
                afterClose: function() {
                    currentScope.saveLog(log);
                }
            });
    };
});