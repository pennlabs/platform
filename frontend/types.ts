/* eslint-disable camelcase */
export interface NamedObject {
    name: string;
    id: number;
}

export interface Major extends NamedObject {
    degree_type: string;
}

export interface Student {
    major: Major[];
    school: NamedObject[];
    graduation_year: number;
}

export interface ContactInfo {
    id: number;
    value: string;
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
    emails: ContactInfo[];
    phone_numbers: ContactInfo[];
}

export enum ContactType {
    Email = "email",
    PhoneNumber = "phonenumber",
}
/**
 * Used for Select
 */
export interface Option {
    label: string;
    value: number;
}
