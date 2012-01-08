String.prototype.format = function () {
    var formatted = this;
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{' + i + '\\}', 'gi');
        formatted = formatted.replace(regexp, arguments[i]);
    }
    return formatted;
};

function EloggerListController($xhr) {
    this.MAX_AUTO_FETCH_NUM = 12;
    this.$xhr = $xhr;
    this.logs = [];
    this.monthsFetched = 0;
    this.lastLoadedDate = null;
}

EloggerListController.prototype = {
    initialize:function () {
        var me = this;
        var today = $.date();
        me.load(today.year(), today.month(), me.loadNextMonth);
        $(window).scroll(function () {
            if (!me.isLoading && $(window).scrollTop() > ($(document).height() - $(window).height() - 3)
                && me.autoLoad()) {
                me.loadNextMonth();
            }
        });
    },
    load:function (year, month, callback) {
        var me = this;
        me.$eval();
        me.isLoading = true;
        me.$xhr("GET", '/logs?year=' + year + '&month=' + month, function (code, data) {
            var monthLogs = me.monthLogs(year, month);
            _.each(monthLogs, function (log) {
                log.content = data["" + log.index];
                me.logs.push(log);
            });
            me.monthsFetched += 1;
            me.isLoading = false;
            me.$eval();
            if(callback){
                callback();
            }
        });
    },
    loadNextMonth:function(){
        var loadStart = this.lastLoadedDate.adjust("D", -1);
        this.load(loadStart.year(), loadStart.month());
    },
    autoLoad:function () {
        return this.monthsFetched < this.MAX_AUTO_FETCH_NUM;
    },
    monthLogs:function (year, month) {
        var me = this;
        var today = $.date();
        var cur = $.date('{0}-{1}-01'.format(year, month), "yyyy-MM-dd");
        me.lastLoadedDate = cur.clone();
        var result = [];
        while (cur.month() === month && cur.year() === year && today.date().getTime() >= cur.date().getTime()) {
            result.push({
                date:cur.format(),
                index:cur.date().getDate()
            });
            cur.adjust("D", 1);
        }
        return result.reverse();
    },
    saveLog:function (log){
        var me=this;
        //log format is {
        me.$xhr("PUT", '/logs', log, function (code, data) {

        });
    },
    editLog: function(log){
        console.log(log)
//         var $this = $(this);
//                $('#edit_log_title').val($this.closest('.log').find('.log_title span').text());
//                $('#edit_log_content').html($this.closest('.log').find('.log_content pre').text());
    }
};

EloggerListController.$inject = ['$xhr'];