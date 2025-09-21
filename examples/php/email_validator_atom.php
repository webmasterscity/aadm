<?php
/**
 * Atom: validar formato de email en PHP.
 *
 * Devuelve un arreglo con claves `valid` y `error` para mantener compatibilidad con
 * las composiciones declarativas descritas en AADM 2.0.
 */
function validate_email_atom(string $email): array
{
    $valid = filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
    return [
        'valid' => $valid,
        'error' => $valid ? null : 'Invalid format',
    ];
}
