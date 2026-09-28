class InvalidRankingError(ValueError):
    """Raised when a submitted ranking breaks the category rules."""


def validate_ranking(club_ids: list[int], pool_club_ids: set[int], ranking_size: int) -> None:
    if len(club_ids) != ranking_size:
        raise InvalidRankingError(
            f"Ranking must contain exactly {ranking_size} clubs, got {len(club_ids)}"
        )
    if len(set(club_ids)) != len(club_ids):
        raise InvalidRankingError("Ranking contains duplicate clubs")
    outside_pool = set(club_ids) - pool_club_ids
    if outside_pool:
        raise InvalidRankingError(f"Clubs not in the category pool: {sorted(outside_pool)}")


def tail_position(ranking_size: int, pool_size: int) -> float:
    """Average of the positions after the Top N (spec 4.1). Pool 25, top 20 -> 23."""
    return (ranking_size + 1 + pool_size) / 2


def effective_positions(
    club_ids: list[int], pool_club_ids: set[int], ranking_size: int
) -> dict[int, float]:
    """Position of every pool club: chosen position, or the tail position if left out."""
    tail = tail_position(ranking_size, len(pool_club_ids))
    chosen = {club_id: position for position, club_id in enumerate(club_ids, start=1)}
    return {club_id: float(chosen.get(club_id, tail)) for club_id in pool_club_ids}