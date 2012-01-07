function EloggerListController($xhr) {
    this.$xhr = $xhr;
    this.logs = [];
}

EloggerListController.prototype = {
    initialize:function(){
      var date=$.date();
      this.fetch(date.year(),date.month());
    },
    fetch:function(year, month) {
        var me = this;
        var getMonthEmptyLogs = function() {
            return [
                {date:"2011-2-11",index:11},
                {date:"2011-2-12",index:12},
                {date:"2011-2-13",index:13},
                {date:"2011-2-14",index:14},
                {date:"2011-2-15",index:15},
                {date:"2011-2-16",index:16},
                {date:"2011-2-17",index:17}
            ]
        }
        var appendToPage = function(data) {
            var monthLogs = getMonthEmptyLogs();
            _.each(monthLogs, function(log) {
                log.content = data[""+log.index];
                me.logs.push(log);
            });
        };
        me.$xhr("GET", '/api/logs?year=' + year + '&month=' + month, function(code, data) {
            appendToPage(data);
        });
    }
}
EloggerListController.$inject = ['$xhr'];