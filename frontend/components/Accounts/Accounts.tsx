import React, { useState } from "react";
import { Field, Form, Formik } from "formik";
import { Heading, Panel } from "react-bulma-components";
import parsePhoneNumber from "libphonenumber-js";
import { useResource } from "@pennlabs/rest-hooks";
import { ContactType, User } from "../../types";
import { doApiRequest } from "../../utils/fetch";
import {
    createContact,
    generateLoadOption,
} from "../../data-fetching/accounts";
import SelectField from "./SelectField";
import VerificationModal from "./Verification/VerificationModal";
import { logException } from "../../utils/sentry";

interface VerificationState {
    type: ContactType;
    id: number;
    contact: string;
}

const Accounts = ({ user: initialUser }: { user: User }) => {
    // User State
    const { data: userPartial, mutate } = useResource<User>("/accounts/me/", {
        initialData: initialUser,
    });
    // TODO: this feels weird
    const user = userPartial!;

    // Verification State + Functions
    const [showVerificationModal, setShowVerificationModal] = useState<boolean>(
        false
    );
    const [verificationState, setVerificationState] = useState<
        VerificationState | undefined
    >(undefined);
    const openVerificationModal = ({
        verified,
        ...props
    }: VerificationState & { verified: boolean }) => {
        if (!verified) {
            setVerificationState(props);
            setShowVerificationModal(true);
        }
    };

    // Contact Method manipulation
    const addContactMethod = async (props: {
        type: ContactType;
        value: string;
    }) => {
        const { type, value } = props;
        try {
            await createContact(type, value);
            mutate();
        } catch (e) {
            logException(e);
            // TODO: toast
        }
    };

    return (
        <div>
            {verificationState && (
                <VerificationModal
                    type={verificationState.type}
                    id={verificationState.id}
                    contact={verificationState.contact}
                    show={showVerificationModal}
                    mutate={mutate}
                    closeFunc={() => setShowVerificationModal(false)}
                />
            )}
            <Heading>Hello, {user.first_name}</Heading>
            <Formik
                initialValues={user}
                onSubmit={(values, actions) => {
                    // TODO: use mutate instead of explicit doApiRequest?
                    doApiRequest("/accounts/me/", {
                        method: "PATCH",
                        body: values,
                    }).catch((err) => console.log(err));
                    // TODO: better error checking (toast?)
                    console.log({ values, actions });
                    actions.setSubmitting(false);
                }}
            >
                <Form>
                    <br />
                    Name: {user.first_name} {user.last_name}
                    <br />
                    PennKey: {user.username}
                    <br />
                    <label htmlFor="first_name">Display Name</label>
                    <Field name="first_name" className="form-input" />
                    <br />
                    <b>Phone Numbers:</b>
                    <br />
                    {user.phone_numbers.length !== 0 &&
                        user.phone_numbers.map((number) => {
                            const prettyPhoneNumber = parsePhoneNumber(
                                number.phone_number
                            )!.formatInternational(); // Safe because this was already validated when added
                            return (
                                <Panel>
                                    <Panel.Block
                                        disabled={true}
                                        onClick={() =>
                                            openVerificationModal({
                                                type: ContactType.PhoneNumber,
                                                id: number.id,
                                                contact: prettyPhoneNumber,
                                                verified: number.verified,
                                            })
                                        }
                                        renderAs="a"
                                    >
                                        {prettyPhoneNumber} -{" "}
                                        {!number.verified && "Not "} Verified
                                    </Panel.Block>
                                </Panel>
                            );
                        })}
                    + Add another phone number
                    <br />
                    <b>Emails:</b>
                    <br />
                    {user.emails.length !== 0 &&
                        user.emails.map((email) => (
                            <Panel>
                                <Panel.Block
                                    disabled={true}
                                    onClick={() =>
                                        openVerificationModal({
                                            type: ContactType.Email,
                                            id: email.id,
                                            contact: email.email,
                                            verified: email.verified,
                                        })
                                    }
                                    renderAs="a"
                                >
                                    {email.email} - {!email.verified && "Not "}{" "}
                                    Verified
                                </Panel.Block>
                            </Panel>
                        ))}{" "}
                    + Add another email
                    <br />
                    {user.groups.includes("student") && (
                        <div>
                            <b>Student:</b>
                            <br />
                            <label htmlFor="student.graduation_year">
                                Graduation Year
                            </label>
                            <Field
                                name="student.graduation_year"
                                className="form-input"
                            />
                            <Field
                                name="student.major"
                                component={SelectField}
                                loadOptions={generateLoadOption("majors")}
                            />
                            <Field
                                name="student.school"
                                component={SelectField}
                                loadOptions={generateLoadOption("schools")}
                            />
                        </div>
                    )}
                    <button type="submit">Submit</button>
                </Form>
            </Formik>
        </div>
    );
};
export default Accounts;

// TODO: figure out a resend verification code flow
// TODO: toasts
// TODO: add contact flow
// TODO: delete contact modal/confirmation
// TODO: make primary button
