"""sink data

Revision ID: 4335b2f797a6
Revises: 57534efe22bb
Create Date: 2023-10-23 19:19:10.372220

"""
from alembic import op

from core.config import get_settings
from core.settings import EnvironmentTypes

# revision identifiers, used by Alembic.
revision = "4335b2f797a7"
down_revision = "cc237cf81664"
branch_labels = None
depends_on = None


def upgrade() -> None:
    if get_settings().environment in (EnvironmentTypes.test, EnvironmentTypes.local):
        op.execute(
            """
        INSERT INTO events (token, administrator_token, name, description, coefficient, created_at, status, expiration_at)
        VALUES
            ('11111111-1111-1111-1111-111111111111', 'admin1', 'Event 1', 'Description for Event 1', 2.0, '2023-10-24 14:00:00', 'SCHEDULED', '2027-10-24 15:00:00'),
            ('22222222-2222-2222-2222-222222222222', 'admin1', 'Event 2', 'Description for Event 2', 1.5, '2023-10-24 14:15:00', 'RIGHT_VICTORY', '2027-10-24 15:15:00'),
            ('33333333-3333-3333-3333-333333333333', 'admin1', 'Event 3', 'Description for Event 3', 3.0, '2023-10-24 14:30:00', 'LEFT_VICTORY', '2023-10-24 15:30:00');
        """
        )


def downgrade() -> None:
    if get_settings().environment in (EnvironmentTypes.test, EnvironmentTypes.local):
        op.execute(
            """
            TRUNCATE
                public.events
                CASCADE;
            """
        )
