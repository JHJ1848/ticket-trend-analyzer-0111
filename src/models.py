from dataclasses import dataclass
from datetime import datetime

@dataclass
class Ticket:
    ticket_id: str
    created_at: datetime
    category: str
    description: str
    priority: str
    resolution_time_hours: float
    satisfaction: int
    channel: str
    is_resolved: bool
    date_str: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Ticket':
        created_dt = datetime.strptime(data['created_at'], '%Y-%m-%d %H:%M')
        return cls(
            ticket_id=data['ticket_id'],
            created_at=created_dt,
            category=data['category'],
            description=data['description'],
            priority=data['priority'],
            resolution_time_hours=float(data['resolution_time_hours']),
            satisfaction=int(data['satisfaction']),
            channel=data['channel'],
            is_resolved=bool(data['is_resolved']),
            date_str=created_dt.strftime('%Y-%m-%d')
        )
