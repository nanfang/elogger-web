String.prototype.format = function () {
    var formatted = this;
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{' + i + '\\}', 'gi');
        formatted = formatted.replace(regexp, arguments[i]);
    }
    return formatted;
};

var DAY_LOG_DAILY = 0;
var DAY_LOG_RETRO = 1;


function EloggerListController($xhr) {
    this.MAX_AUTO_FETCH_NUM = 36;
    this.$xhr = $xhr;
    this.logs = [];
    this.monthsFetched = 0;
    this.lastLoadedDate = null;
    this.autoLoading = true;
    this.isLoading = false;
}

EloggerListController.prototype = {
    initialize:function () {
        var me = this;
        var today = $.date();
        me.load(today.year(), today.month(), me.loadNextMonth);
        if (me.autoLoading) {
            $(window).scroll(function () {
                if (!me.isLoading && $(window).scrollTop() > ($(document).height() - $(window).height() - 3)
                    && me.isScrolling()) {
                    me.loadNextMonth();
                }
            });
        }
    },
    raw_log:function (date) {
        return {
            id:"",
            title:date.format("yyyy-MM-dd"),
            index:"unsaved-" + date.format("yyyyMMdd"),
            status:'saved',
            day:date.date().getDate(),
            month:date.month(),
            year:date.year(),
            weekDay:date.date().getDay(),
            type:DAY_LOG_DAILY
        };
    },

    current_date:function (year, month) {
        var cur = null;
        var today = $.date();
        if (year === today.year() && month === today.month()) {
            cur = today;
        } else if (!(year > today.year() || (year === today.year() && month > today.month()))) {
            cur = $.date('{0}-{1}-01'.format(year, month), "yyyy-MM-dd");
            cur.adjust("M", 1);
            cur.adjust("D", -1);
        }
        return cur;
    },

    load:function (year, month, callback) {
        var me = this;
        me.isLoading = true;
        me.$eval();
        me.$xhr("GET", '/logs?year=' + year + '&month=' + month, function (code, data) {
            var cur = me.current_date(year, month);
            if (!cur) {
                return;
            }

            while (cur.month() === month && cur.year() === year) {
                var logs = data["" + cur.date().getDate()];
                if (logs) {
                    _.each(logs, function (log) {
                        var day_log = me.raw_log(cur);
                        day_log.id = log.id;
                        day_log.index = "saved-"+log.id;
                        day_log.type = log.type;
                        day_log.content = log.content;
                        if (log.type != DAY_LOG_DAILY) {
                            day_log.title = log.title;
                        }
                        me.logs.push(day_log);
                    });
                } else {
                    me.logs.push(me.raw_log(cur));
                }
                me.lastLoadedDate = cur;
                cur.adjust("D", -1);
            }
            me.monthsFetched += 1;
            me.isLoading = false;
            me.$eval();
            if (callback) {
                callback();
            }
        });
    },
    loadNextMonth:function () {
        var loadStart = this.lastLoadedDate.adjust("D", -1);
        this.load(loadStart.year(), loadStart.month());
    },
    isScrolling:function () {
        return this.monthsFetched < this.MAX_AUTO_FETCH_NUM;
    },
    saveLog:function (log) {
        var me = this;
        $("#"+log.index).show(1000);
        me.$eval();
        me.$xhr("POST", '/logs', {
            id:log.id,
            type:log.type,
            day:log.day,
            month:log.month,
            year:log.year,
            title:log.title,
            content:log.content
        }, function (code, data) {
            $("#"+log.index).hide(1000);
            log.id=data;
            log.index = "saved-"+log.id;
            me.$eval();
        });
    }
};

EloggerListController.$inject = ['$xhr'];