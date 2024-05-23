"""empty message

Revision ID: 545980672560
Revises: 05bfb383a0c3
Create Date: 2024-05-23 21:16:12.114247

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '545980672560'
down_revision = '05bfb383a0c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Deploy', schema=None) as batch_op:
        batch_op.drop_constraint('deploy_ibfk_2', type_='foreignkey')
        batch_op.drop_column('project_id')

    with op.batch_alter_table('Project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_build_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('current_deployment_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('project_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Deploy', ['current_deployment_id'], ['id'])
        batch_op.create_foreign_key(None, 'Build', ['current_build_id'], ['id'])
        batch_op.drop_column('deploy_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deploy_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('project_ibfk_2', 'Deploy', ['deploy_id'], ['id'])
        batch_op.drop_column('current_deployment_id')
        batch_op.drop_column('current_build_id')

    with op.batch_alter_table('Deploy', schema=None) as batch_op:
        batch_op.add_column(sa.Column('project_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('deploy_ibfk_2', 'Project', ['project_id'], ['id'])

    # ### end Alembic commands ###