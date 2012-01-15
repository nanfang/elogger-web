angular.directive('my:fancybox', function (expression, compiledElement) {
    var compiler = this;
    return function (linkElement) {
        var currentScope = this;
        var log = currentScope.log;
        $(linkElement).fancybox({
            maxWidth:732,
            maxHeight:423,
            padding:0,
            fitToView:false,
            width:'100%',
            height:'100%',
            autoSize:false,
            closeClick:false,
            openEffect:'elastic',
            closeEffect:'fade',
            beforeLoad:function () {
                this.title = log.title;
            },
            afterClose:function () {
                currentScope.saveLog(log);
            }
        });
    };
});