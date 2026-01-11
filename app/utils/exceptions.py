class CalendarEventCreationError(Exception):
    def __init__(self, message="Error occurred during creation process"):
        self.message = message
        super().__init__(self.message)

class CalendarEventUpdateError(Exception):
    def __init__(self, message="Error occurred during update process"):
        self.message = message
        super().__init__(self.message)

class CalendarEventDeletionError(Exception):
    def __init__(self, message="Error occurred during deletion process"):
        self.message = message
        super().__init__(self.message)
class CalendarDailyReportError(Exception):
    def __init__(self, message="Error occurred during daily report generation"):
        self.message = message
        super().__init__(self.message)

class EventNotFoundError(Exception):
    def __init__(self, message="Event not found"):
        self.message = message
        super().__init__(self.message)
class EventConflictError(Exception):
    def __init__(self, message="Event conflict detected"):
        self.message = message
        super().__init__(self.message)

class CalendarAvailabilityError(Exception):
    def __init__(self, message="Error occurred during availability check"):
        self.message = message
        super().__init__(self.message)

class EventNotFoundError(Exception):
    def __init__(self, message="Event not found"):
        self.message = message
        super().__init__(self.message)