wpsc = {
    timer_handle: null,
    check: function(guid) {
        this.do_actual_check(guid);
        wpsc.timer_handle = window.setInterval(this.do_actual_check, 2000, guid);
    },
    do_actual_check: function(guid) {
        $.getJSON("/check/" + guid, function(data) {
            if (data.status == 'processing') {
                $('#results').html('Processing... hold on.');
            } else if (data.status == 'error') {
                $('#results').html('There was an error retrieving information for this app. Please, contact the developer using the link below.');
                window.clearInterval(wpsc.timer_handle);
            } else if (data.status == 'done') {
                $('#results').html(data.results);
                $('#wait').html('You can sort the columns of the table by clicking the headers.')
                $('#sortable').tablesorter();
                window.clearInterval(wpsc.timer_handle);
            }
        });
    },
    launch: function(guid) {
        var matches = guid.match(/[0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{12}/);
        if (matches) {
            $("#warning").hide();
            window.location.href = '/app/' + matches[0];
        } else {
            $("#warning").show();
        }
    }
}
$(document).ready(function() {
    $.tablesorter.addParser({
        id: 'aryan',
        is: function(s, table) {
            var c = table.config;
            return $.tablesorter.isDigit(s.replace(new RegExp(/\s.*$/g), ''), c);
        },
        format: function (s) {
            return $.tablesorter.formatFloat(s.replace(new RegExp(/\s.*$/g), ''));
        },
        type: "numeric",
    });

    $("#email").html(atob("d29kaW1Adm9ydGlnYXVudC5uZXQ="));
});