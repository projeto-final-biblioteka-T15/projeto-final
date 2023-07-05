from django.db import models
from books.models import Book

from django.utils import timezone
from loans.models import Loan
from datetime import timedelta


class Copies(models.Model):
    total = models.PositiveIntegerField(default=1)
    available = models.PositiveIntegerField(default=1)

    book = models.ForeignKey(Book, related_name="copies", on_delete=models.CASCADE)

    def loan_copy(self):
        if self.available > 0:
            self.available -= 1
            self.save()
        else:
            raise Exception("Não há cópias disponíveis para empréstimo.")

    def return_copy(self):
        self.available += 1
        self.save()

        loan = Loan.objects.filter(copy=self, return_date__lt=timezone.now()).first()
        if loan:
            # O livro foi devolvido após a data de retorno estipulada
            loan.user.is_blocked = True
            loan.user.blocked_until = timezone.now() + timedelta(
                days=7
            )  # Bloqueia o usuário por 7 dias
            loan.user.save()
