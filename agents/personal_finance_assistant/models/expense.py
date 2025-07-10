import uuid

from datetime import date as python_date
from datetime import time as python_time

from pydantic import BaseModel, Field


class ExpenseCategory(BaseModel):
    """Represents a category for classifying expenses.

    Fields:
        id (uuid.UUID): Unique identifier for the expense category.
        name (str): Name of the expense category.
    """

    id: uuid.UUID | None = Field(
        description='id of the expense category',
        default_factory=uuid.uuid4,
    )
    name: str = Field(description='name of the expense category')


class Expense(BaseModel):
    """Represents an individual expense entry.

    Fields:
        id (uuid.UUID): Unique identifier for the expense.
        amount (float): Amount of the expense.
        date (datetime.date): Date when the expense occurred.
        time (datetime.time): Time when the expense occurred.
        category (ExpenseCategory): Category associated with the expense.
    """

    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, description='id of the expense'
    )
    description: str = Field(description='description of the expense')
    amount: float = Field(description='amount of the expense')
    date: python_date = Field(description='date of the expense')
    time: python_time = Field(description='time of the expense')
    category: ExpenseCategory = Field(description='category of the expense')
