from datetime import date as python_date
from datetime import time as python_time

from pydantic import BaseModel, Field


class Expense(BaseModel):
    """Represents a single expense entry.

    Attributes:
        category (str): The category of the expense (e.g., groceries, rent).
        amount (float): The amount spent.
        date (date): The date when the expense occurred.
        time (time): The time when the expense occurred.
        note (Optional[str]): An optional note or description for the expense.
    """

    category: str = Field(
        default='unknown', description='category of the expense'
    )
    amount: float = Field(default=0, description='amount of the expense')
    date: python_date = Field(
        default=python_date.today(), description='date of the expense'
    )
    time: python_time = Field(
        default=python_time(), description='time of the expense'
    )
    note: str | None = Field(default=None, description='note for the expense')
