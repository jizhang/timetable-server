var Event = function(opts) {
	var self = this;
	self.contextPath = opts.contextPath;
	$(function() {
		self.init();
	});
};

Event.prototype = {
	constructor: Event,

	calcHeight: function() {
		return $(window).height() - 50;
	},

	init: function() {
		var self = this;

		$('#calendar').fullCalendar({

			height: self.calcHeight(),
			defaultView: 'agendaWeek',
			firstDay: 1,
			allDaySlot: false,
			slotLabelFormat: 'HH:mm',
			timeFormat: 'HH:mm',
			scrollTime: '08:00:00',
			events: self.contextPath + '/event/list',

			selectable: true,
			selectHelper: true,
			select: function(start, end) {
				var title = prompt('Event Title:');
				if (!title) {
					$('#calendar').fullCalendar('unselect');
					return;
				}

				var eventData = {
					title: title,
					start: start.format('YYYY-MM-DD HH:mm:ss'),
					end: end.format('YYYY-MM-DD HH:mm:ss')
				};

				$.post(self.contextPath + '/event/add', eventData, function(result) {

					if (result.status != 'ok') {
						alert(result.msg);
						return;
					}

					eventData.id = result.id;
					$('#calendar').fullCalendar('renderEvent', eventData);
					$('#calendar').fullCalendar('unselect');
				});

			},

			eventClick: function(event) {
				if (confirm('Delete this event?')) {

					var data = {
						id: event.id
					};

					$.post(self.contextPath + '/event/delete', data, function(result) {
						if (result.status != 'ok') {
							alert(result.msg);
						}
						$('#calendar').fullCalendar('removeEvents', event.id);
					});
				}
			}
		});

		$(window).resize(function() {
			$('#calendar').fullCalendar('option', 'height', self.calcHeight());
		});
	},

	_theEnd: undefined
};
