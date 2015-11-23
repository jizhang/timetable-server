var Event = function(opts) {
	var self = this;
	self.contextPath = opts.contextPath;
	$(function() {
		self.init();
	});
};

Event.prototype = {
	constructor: Event,

	formatDate: function(dt) {
		return dt.format('YYYY-MM-DD HH:mm:ss');
	},

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
			editable: true,
			selectable: true,
			selectHelper: true,

			select: function(start, end) {
				var title = prompt('Event Title:');
				if (!title) {
					$('#calendar').fullCalendar('unselect');
					return;
				}

				var data = {
					title: title,
					start: self.formatDate(start),
					end: self.formatDate(end)
				};

				$.post(self.contextPath + '/event/save', data, function(result) {

					if (result.status != 'ok') {
						alert(result.msg);
						return;
					}

					data.id = result.id;
					$('#calendar').fullCalendar('renderEvent', data);
					$('#calendar').fullCalendar('unselect');
				});

			},

			eventClick: function(event) {
				$('#txtTitle').val(event.title);
				$('#dlgEvent').data('event', event);
				$('#dlgEvent').dialog('open');
			},

			eventDrop: function(event, delta, revertFunc) {
				self.saveEvent(event, revertFunc);
			},

			eventResize: function(event, delta, revertFunc) {
				self.saveEvent(event, revertFunc);
			}
		});

		$(window).resize(function() {
			$('#calendar').fullCalendar('option', 'height', self.calcHeight());
		});

		$('#dlgEvent').dialog({
			autoOpen: false,
			width: 400,
			height: 300,
			modal: true,
			buttons: {
				'Save': function() {

					var event = $('#dlgEvent').data('event');
					var title = $('#txtTitle').val();

					if (title) {

						var oldTitle = event.title;
						event.title = title;
						$('#calendar').fullCalendar('updateEvent', event);

						self.saveEvent(event, function() {
							event.title = oldTitle;
							$('#calendar').fullCalendar('updateEvent', event);
						});

					}

					$('#dlgEvent').dialog('close');

				},
				'Delete': function() {

					var event = $('#dlgEvent').data('event');

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

					$('#dlgEvent').dialog('close');

				},
				'Cancel': function() {
					$('#dlgEvent').dialog('close');
				}
			}
		});

	},

	saveEvent: function(event, revertFunc) {
		var self = this;

		var data = {
			id: event.id,
			title: event.title,
			start: self.formatDate(event.start),
			end: self.formatDate(event.end)
		};

		$.post(self.contextPath + '/event/save', data, function(result) {
			if (result.status != 'ok') {
				alert(result.msg);
				revertFunc();
				return;
			}
		});
	},

	_theEnd: undefined
};
