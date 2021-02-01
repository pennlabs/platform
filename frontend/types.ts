export interface Major {
    id: number;
    name: string;
}
export interface Student {
    major: Major[];
}

export interface Email {
    id: number;
    email: string;
    primary: boolean;
    verified: boolean;
}

export interface PhoneNumber {
    id: number;
    phone_number: string;
    primary: boolean;
    verified: boolean;
}

export interface User {
    pennid: number;
    first_name: string;
    last_name: string;
    username: string;
    email: string;
    groups: string[];
    product_permissions: string[];
    user_permissions: string[];
    student: Student;
    emails: Email[];
    phone_numbers: PhoneNumber[];
}

/**
 * Used for Select
 */
export interface Option {
    label: string;
    value: string;
}
