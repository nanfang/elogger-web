

String.prototype.format = function () {
    var formatted = this;
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{' + i + '\\}', 'gi');
        formatted = formatted.replace(regexp, arguments[i]);
    }
    return formatted;
};

function EloggerListController($xhr) {
    this.MAX_AUTO_FETCH_NUM = 36;
    this.$xhr = $xhr;
    this.logs = [];
    this.monthsFetched = 0;
    this.lastLoadedDate = null;
    this.autoLoading=true;
    this.isLoading=false;
}

EloggerListController.prototype = {
    initialize:function () {
        var me = this;
        var today = $.date();
        me.load(today.year(), today.month(), me.loadNextMonth);
        if(me.autoLoading){
            $(window).scroll(function () {
                if (!me.isLoading && $(window).scrollTop() > ($(document).height() - $(window).height() - 3)
                    && me.isScrolling()) {
                    me.loadNextMonth();
                }
            });
        }
    },
    load:function (year, month, callback) {
        var me = this;
        me.$eval();
        me.isLoading = true;
        me.$eval();
        me.$xhr("GET", '/logs?year=' + year + '&month=' + month, function (code, data) {
            var monthLogs = me.monthLogs(year, month);
            _.each(monthLogs, function (log) {
                log.content = data["" + log.index];
                me.logs.push(log);
            });
            me.monthsFetched += 1;
            me.isLoading = false;
            me.$eval();
            if (callback) {
                callback();
            }
        });
    },
    loadNextMonth:function() {
        var loadStart = this.lastLoadedDate.adjust("D", -1);
        this.load(loadStart.year(), loadStart.month());
    },
    isScrolling:function () {
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
                title:cur.format(),
                index:cur.date().getDate(),
                status:'saved',
                day:cur.date().getDate(),
                month:cur.month(),
                year:cur.year(),
                weekDay:cur.date().getDay()

            });
            cur.adjust("D", 1);
        }
        return result.reverse();
    },
    saveLog:function (log) {
        var me = this;
        console.log("log saved:", log);
        log.status='saving';
        var saving = $('#saving_log_{0}_{1}_{2}'.format(log.year, log.month, log.day));

        saving.show('slow');
        me.$xhr("POST", '/logs', {
            day:log.day,
            month:log.month,
            year:log.year,
            content:log.content
        }, function (code, data) {
            saving.hide();
        });
    }

};

EloggerListController.$inject = ['$xhr'];