"""init_migration

Revision ID: cc237cf81664
Revises:
Create Date: 2023-10-23 12:01:31.339819

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "cc237cf81664"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "events",
        sa.Column("token", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("administrator_token", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("coefficient", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column(
            "status",
            sa.Enum("SCHEDULED", "PENDING", "RIGHT_VICTORY", "LEFT_VICTORY", name="eventstatus"),
            nullable=False,
        ),
        sa.Column("status_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("token"),
    )
    op.create_index(
        "events_administrator_token_created_at_idx", "events", ["administrator_token", "created_at"], unique=False
    )
    # ### end Alembic commands ###

    op.execute(
        """
        CREATE FUNCTION public.refresh_status_updated_at()
        RETURNS TRIGGER
        LANGUAGE plpgsql AS
        $func$
        BEGIN
           NEW.status_updated_at := now();
           RETURN NEW;
        END
        $func$;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trig_request_status_updated BEFORE UPDATE OF status ON public.events
            FOR EACH ROW EXECUTE PROCEDURE public.refresh_status_updated_at();
        """
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("events_administrator_token_created_at_idx", table_name="events")
    op.drop_table("events")
    # ### end Alembic commands ###
    op.execute("DROP FUNCTION public.refresh_status_updated_at CASCADE;")