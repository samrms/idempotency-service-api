from src.infrastructure.repositories import SqlAlchemyIdempotencyRepository


def test_idempotency_key_is_persisted_with_unique_constraint():
    from src.infrastructure.database.session import SessionLocal

    with SessionLocal() as session:
        repository = SqlAlchemyIdempotencyRepository(session)
        assert repository.reserve("repository-key", "a" * 64) is None
        repository.save_result("repository-key", "a" * 64, 201, {"id": "operation"})
        existing = repository.reserve("repository-key", "a" * 64)
        assert existing is not None
        assert existing.status_code == 201
        session.rollback()
