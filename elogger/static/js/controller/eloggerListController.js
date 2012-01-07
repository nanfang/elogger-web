function EloggerListController($xhr) {
    this.$xhr = $xhr;
    this.logs = [];
}

EloggerListController.prototype = {
    initialize:function() {
        var date = $.date();
        this.fetch(date.year(), date.month());
    },
    fetch:function(year, month) {
        var me = this;
        var getMonthEmptyLogs = function() {
            var today = $.date();
            var result = [];
            var currentDay = $.date().setYear(year).setMonth(month).setDay(1);
            while (currentDay.month() === month && today.date().getTime() >= currentDay.date().getTime()) {
                result.push({
                    date:currentDay.format("yyyy-MM-dd"),
                    index:currentDay.dateNum()
                });
                currentDay.adjust("D", 1);
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
        me.$xhr("GET", '/api/logs?year=' + year + '&month=' + month, function(code, data) {
            appendToPage(data);
            me.lastFetchedDate = $.date().setYear(year).setMonth(month).setDay(1);
        });
    },
    fetchNextMonth:function() {
        var dateToFetch = this.lastFetchedDate.adjust("D", -1);
        this.fetch(dateToFetch.year(), dateToFetch.month());
    }
};

EloggerListController.$inject = ['$xhr'];