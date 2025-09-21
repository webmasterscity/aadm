/// Atom: validar email en Flutter/Dart.
/// Se modela como función pura para facilitar pruebas y composición.
const String emailPattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$';

typedef EmailValidationResult = Map<String, Object?>;

EmailValidationResult validateEmailAtom(String email) {
  final regex = RegExp(emailPattern);
  final isValid = regex.hasMatch(email);
  return {
    'valid': isValid,
    'error': isValid ? null : 'Invalid format',
  };
}
