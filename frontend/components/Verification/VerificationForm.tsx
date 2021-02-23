import React, { useRef } from "react";
import ReactCodeInput from "react-code-input";
import { mutateResourceFunction } from "@pennlabs/rest-hooks/dist/types";
import { verifyContact } from "../../data-fetching/accounts";
import { ContactType, User } from "../../types";
import { logException } from "../../utils/sentry";

// TODO: combine some of these types
interface VerificationFormProps {
    type: ContactType;
    id: number;
    closeFunc: () => void;
    mutate: mutateResourceFunction<User>;
    // toastFunc: (Toast) => void;
}

interface CodeInputRefState {
    input: string[];
}

interface CodeInputRef extends ReactCodeInput {
    textInput: HTMLInputElement[];
    value: string;
    state: CodeInputRefState;
}

const VerificationForm = (props: VerificationFormProps) => {
    const { type, id, closeFunc, mutate } = props;
    const codeInput = useRef<CodeInputRef>(null);
    const handleInputChange = async (value: string) => {
        if (value.length === 6) {
            try {
                await verifyContact(type, id, value);
                closeFunc();
                mutate();
                // TODO: toast
            } catch (e) {
                logException(e);
                // TODO: toast
            }
        }
    };
    return (
        <ReactCodeInput
            name="verification"
            fields={6}
            onChange={handleInputChange}
            ref={codeInput}
            inputMode="numeric"
        />
    );
};

export default VerificationForm;
