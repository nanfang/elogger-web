function EloggerListController($xhr) {
    this.$xhr = $xhr;
    this.logs = [];
}

EloggerListController.prototype = {
    initialize:function() {
        var me = this;
        var date = $.date();
        me.isLoading = false;
        me.fetch(date.year(), date.month(), 2);
        $(window).scroll(function() {
            if ($(window).scrollTop() > ($(document).height() - $(window).height() - 3)) {
                me.fetchNextMonth();
            }
        });
    },
    fetch:function(year, month, monthNum, waitTime) {
        monthNum = monthNum || 1;
        waitTime=waitTime||0;
        var me = this;
        var getMonthEmptyLogs = function() {
            var today = $.date();
            var result = [];
            var currentDay = $.date().setYear(year).setMonth(month).setDay(1).adjust("M", -monthNum + 1);
            var currentMonth = currentDay.month();
            for (var i = 0; i < monthNum; i++) {
                while (currentDay.month() === currentMonth && today.date().getTime() >= currentDay.date().getTime()) {
                    result.push({
                        date:currentDay.format("yyyy-MM-dd"),
                        index:currentDay.dateNum()
                    });
                    currentDay.adjust("D", 1);
                }
                currentMonth = currentDay.month();
            }
            return result.reverse();
        };
        var appendToPage = function(data) {
            var monthLogs = getMonthEmptyLogs();
            _.each(monthLogs, function(log) {
                log.content = data["" + log.index];
                me.logs.push(log);
            });
        };
        me.isLoading = true;
        me.$eval();
        me.$xhr("GET", '/api/logs?year=' + year + '&month=' + month + '&monthNum=' + monthNum, function(code, data) {
            me.lastFetchedDate = $.date().setYear(year).setMonth(month).setDay(1).adjust("M", -monthNum + 1);
            setTimeout(function() {
                appendToPage(data);
                me.isLoading = false;
                me.$eval();
            }, waitTime);
        });
    },
    fetchNextMonth:function() {
        var dateToFetch = this.lastFetchedDate.adjust("D", -1);
        this.fetch(dateToFetch.year(), dateToFetch.month(),1, 1000);
    }
};

EloggerListController.$inject = ['$xhr'];