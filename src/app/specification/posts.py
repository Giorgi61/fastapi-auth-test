from app.specification.base import BaseLoadSpecification, BaseWhereSpecification


class PostWhereSpecification(BaseWhereSpecification):

	pass


class PostLoadSpecification(BaseLoadSpecification):


	joinedload: list[str] = ['author']




