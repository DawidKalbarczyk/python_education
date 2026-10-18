"""Testy wiedźmińskiej klasy w Kaer Morhen (pytest)."""

import pytest

from pytest.source.school import Classroom, Person, Student, Teacher, TooManyStudents


# Imiona do zapełnienia sali; Ciri zostaje kandydatką na dodatkowe miejsce.
ADEPCI_KAER_MORHEN = (
    "Eskel", "Lambert", "Coën", "Letho", "Berengar",
    "Leo", "Jaskier", "Milva", "Angoulême", "Triss",
)


@pytest.fixture
def geralt():
    """Nauczyciel szermierki."""
    return Teacher("Geralt z Rivii", 100)


@pytest.fixture
def ciri():
    """Nowa adeptka."""
    return Student("Ciri", 20)


@pytest.fixture
def klasa_w_kaer_morhen(geralt):
    """Niewielka grupa na kursie wiedźmińskim."""
    uczniowie = [Student("Eskel", 95), Student("Lambert", 80)]
    return Classroom(geralt, uczniowie, "Szermierka w Kaer Morhen")


@pytest.fixture
def pelna_klasa(geralt):
    """Dziesięciu adeptów: wszystkie miejsca zajęte."""
    uczniowie = [Student(imie, 20 + i) for i, imie in enumerate(ADEPCI_KAER_MORHEN)]
    return Classroom(geralt, uczniowie, "Próba Traw")


@pytest.mark.parametrize(
    ("typ_postaci", "imie", "wiek"),
    [
        (Person, "Vesemir", 200),
        (Teacher, "Yennefer", 99),
        (Student, "Ciri", 20),
    ],
    ids=["osoba-vesemir", "nauczycielka-yennefer", "uczennica-ciri"],
)
def test_utworzenie_postaci(typ_postaci, imie, wiek):
    postac = typ_postaci(imie, wiek)

    assert postac.name == imie
    assert postac.age == wiek
    assert isinstance(postac, Person)


def test_klasa_zachowuje_nauczyciela_uczniow_i_nazwe(geralt):
    uczniowie = [Student("Eskel", 95)]
    klasa = Classroom(geralt, uczniowie, "Znaki wiedźmińskie")

    assert klasa.teacher is geralt
    assert klasa.students is uczniowie
    assert klasa.course_title == "Znaki wiedźmińskie"


@pytest.mark.parametrize("poczatkowa_liczba", [0, 1, 9], ids=["pusta", "jeden", "dziewiec"])
def test_mozna_dodac_ucznia_gdy_jest_miejsce(geralt, ciri, poczatkowa_liczba):
    uczniowie = [
        Student(imie, 20 + i)
        for i, imie in enumerate(ADEPCI_KAER_MORHEN[:poczatkowa_liczba])
    ]
    klasa = Classroom(geralt, uczniowie, "Szlak wiedźmina")

    klasa.add_student(ciri)

    assert len(klasa.students) == poczatkowa_liczba + 1
    assert klasa.students[-1] is ciri


def test_nie_mozna_dodac_jedenastego_ucznia(pelna_klasa, ciri):
    stan_przed = pelna_klasa.students.copy()

    with pytest.raises(TooManyStudents, match="Cannot add more than 10 students"):
        pelna_klasa.add_student(ciri)

    assert pelna_klasa.students == stan_przed
    assert ciri not in pelna_klasa.students


def test_mozna_usunac_ucznia(klasa_w_kaer_morhen):
    eskel = klasa_w_kaer_morhen.students[0]

    klasa_w_kaer_morhen.remove_student(eskel)

    assert eskel not in klasa_w_kaer_morhen.students
    assert [uczen.name for uczen in klasa_w_kaer_morhen.students] == ["Lambert"]


def test_usuniecie_nieobecnego_ucznia_zglasza_blad(klasa_w_kaer_morhen, ciri):
    stan_przed = klasa_w_kaer_morhen.students.copy()

    # Domyślna reprezentacja obiektu Student zawiera adres pamięci,
    # dlatego sprawdzamy tylko stały fragment komunikatu.
    with pytest.raises(ValueError, match="is not in the classroom"):
        klasa_w_kaer_morhen.remove_student(ciri)

    assert klasa_w_kaer_morhen.students == stan_przed


def test_po_usunieciu_z_pelnej_klasy_mozna_dodac_nowego_ucznia(pelna_klasa, ciri):
    odchodzacy = pelna_klasa.students[0]
    pelna_klasa.remove_student(odchodzacy)

    pelna_klasa.add_student(ciri)

    assert len(pelna_klasa.students) == 10
    assert odchodzacy not in pelna_klasa.students
    assert ciri in pelna_klasa.students


def test_zmiana_nauczyciela(klasa_w_kaer_morhen, geralt):
    vesemir = Teacher("Vesemir", 200)

    klasa_w_kaer_morhen.change_teacher(vesemir)

    assert klasa_w_kaer_morhen.teacher is vesemir
    assert klasa_w_kaer_morhen.teacher is not geralt
    assert klasa_w_kaer_morhen.course_title == "Szermierka w Kaer Morhen"
