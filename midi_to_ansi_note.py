
num2note = {
  0 : "C",
  1 : "C#",
  2 : "D",
  3 : "D#",
  4 : "E",
  5 : "F",
  6 : "F#",
  7 : "G",
  8 : "G#",
  9 : "A",
  10 : "A#",
  11 : "B",
}


def midi_to_ansi_note(n):
  note, number = divmod(n, 12)
  return f"{num2note[note]}{number-1}"