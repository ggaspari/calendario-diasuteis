import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))

from feriados import calendario, feriados, pascoa  # noqa: E402


class TestFeriados(unittest.TestCase):
    def test_pascoa(self):
        self.assertEqual(pascoa(2024), date(2024, 3, 31))
        self.assertEqual(pascoa(2025), date(2025, 4, 20))
        self.assertEqual(pascoa(2026), date(2026, 4, 5))
        self.assertEqual(pascoa(2027), date(2027, 3, 28))

    def test_consciencia_negra_a_partir_de_2024(self):
        self.assertNotIn(date(2023, 11, 20), feriados(2023))
        self.assertIn(date(2024, 11, 20), feriados(2024))

    def test_opcionais(self):
        self.assertNotIn(date(2026, 2, 17), feriados(2026))
        self.assertIn(date(2026, 2, 16), feriados(2026, carnaval=True))
        self.assertIn(date(2026, 2, 17), feriados(2026, carnaval=True))
        self.assertIn(date(2026, 6, 4), feriados(2026, corpus_christi=True))

    def test_calendario_2026(self):
        c = calendario(2026)
        jan = c["meses"][0]
        # Jan/2026: 1 (qui) feriado; 21 dias úteis
        self.assertEqual(jan["dias_uteis"], 21)
        self.assertEqual(jan["quinto_dia_util"], 8)
        self.assertEqual(jan["decimo_dia_util"], 15)
        abril = c["meses"][3]  # Sexta Santa 3/4 e Tiradentes 21/4 (ter)
        self.assertEqual(abril["dias_uteis"], 20)
        self.assertEqual(abril["quinto_dia_util"], 8)
        self.assertEqual(sum(m["dias_uteis"] for m in c["meses"]), c["total_dias_uteis"])


if __name__ == "__main__":
    unittest.main()
