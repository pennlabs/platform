import React, { useState } from "react";
import { Field, Form, Formik } from "formik";
import AsyncSelect from "react-select/async";
import { Heading, Panel } from "react-bulma-components";
import parsePhoneNumber from "libphonenumber-js";
import { useResource } from "@pennlabs/rest-hooks";
import {
  selectStyles,
  RootContainer,
  Button,
  Flex,
  Nav,
  MainContainer,
  CenterContainer,
  Logo,
  FormGroupGrid,
  FormGroupItem,
  Text,
  Break,
  FormGroupHeader,
} from "./ui";
import { FormikInput } from "./Forms/Input";
import { FormikMultipleInputs } from "./Forms/MultipleInput";
import { FormikSelectInput } from "./Forms/SelectInput";
import { ContactType, User } from "../../types";
import { doApiRequest } from "../../utils/fetch";
import {
  createContact,
  generateLoadOption,
} from "../../data-fetching/accounts";
import VerificationModal from "./Verification/VerificationModal";
import { logException } from "../../utils/sentry";
import DeleteModal from "./DeleteModal";

interface ContactMethodState {
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
    ContactMethodState | undefined
  >(undefined);
  const openVerificationModal = ({
    verified,
    ...props
  }: ContactMethodState & { verified: boolean }) => {
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

  // Delete contact method state + functions
  const [showDeleteModal, setShowDeleteModal] = useState<boolean>(false);
  const [deleteState, setDeleteState] = useState<
    ContactMethodState | undefined
  >(undefined);

  return (
    <RootContainer>
      <Nav>
        <Flex margin="1rem" childMargin="0.2rem">
          <Logo src="/beaker.png" />
          <h4>Platform</h4>
        </Flex>
      </Nav>
      <MainContainer>
        <CenterContainer>
          <div>
            {verificationState && (
              <VerificationModal
                type={verificationState.type}
                id={verificationState.id}
                contact={verificationState.contact}
                show={showVerificationModal}
                mutate={mutate}
                closeFunc={() =>
                  setShowVerificationModal(false)
                }
              />
            )}
            {deleteState && (
              <DeleteModal
                type={deleteState.type}
                id={deleteState.id}
                contact={deleteState.contact}
                show={showDeleteModal}
                mutate={mutate}
                closeFunc={() => setShowDeleteModal(false)}
              />
            )}
            <Heading>{`Welcome, ${user.first_name}`}</Heading>
            <Formik
              initialValues={user}
              onSubmit={(values, actions) => {
                mutate(values)
                // TODO: better error checking (toast?)
                console.log({ values, actions });
                actions.setSubmitting(false);
              }}
            >
              <Form style={{ paddingBottom: "3rem" }}>
                <FormGroupGrid>
                  <FormGroupItem col={1} row={1}>
                    <Text weight="400">Name</Text>
                  </FormGroupItem>
                  <FormGroupItem col={2} row={1}>
                    <Text weight="300">
                      {`${user.first_name} ${user.last_name}`}
                    </Text>
                  </FormGroupItem>
                  <FormGroupItem col={1} row={2}>
                    <Text weight="400">Username</Text>
                  </FormGroupItem>
                  <FormGroupItem col={2} row={2}>
                    <Text weight="300">
                      {user.username}
                    </Text>
                  </FormGroupItem>
                  <FormGroupItem col={1} row={3}>
                    <Text weight="400">Display Name</Text>
                  </FormGroupItem>
                  <FormGroupItem col={2} row={3}>
                    <FormikInput
                      fieldName="first_name"
                      type="text"
                    />
                  </FormGroupItem>
                </FormGroupGrid>
                <Break />
                <FormGroupHeader>Contact</FormGroupHeader>
                <FormGroupGrid>
                  <FormGroupItem col={1} row={1} alignItems="start">
                    <Text weight="400" marginTop="0.5rem">Email</Text>
                  </FormGroupItem>
                  <FormGroupItem col={2} row={1} alignItems="start">
                    <Flex flexDirection="column" alignItems="start" childMargin="0.2rem" width="100%">
                      <FormikMultipleInputs route="/accounts/me/email/" initialData={user.emails}
                        addText="Add another email address" contactType={ContactType.Email} />
                    </Flex>
                  </FormGroupItem>
                  <FormGroupItem col={1} row={2} alignItems="start">
                    <Text weight="400" marginTop="0.5rem">Phone Number</Text>
                  </FormGroupItem>
                  <FormGroupItem col={2} row={2} alignItems="start">
                    <Flex flexDirection="column" alignItems="start" childMargin="0.2rem" width="100%">
                      <FormikMultipleInputs route="/accounts/me/phonenumber/" initialData={user.phone_numbers}
                        addText="Add a phone number" contactType={ContactType.PhoneNumber} />
                    </Flex>
                  </FormGroupItem>
                </FormGroupGrid>
                <Break />
                <FormGroupHeader>Academics</FormGroupHeader>
                <FormGroupGrid>
                  <FormGroupItem col={1} row={1}>
                    <Text weight="400">School(s)</Text>
                  </FormGroupItem>
                  <FormGroupItem col={2} row={1}>
                    <FormikSelectInput
                      route="/accounts/schools/"
                      fieldName="student.school"
                    />
                  </FormGroupItem>
                  <FormGroupItem col={1} row={2}>
                    <Text weight="400">Major(s)</Text>
                  </FormGroupItem>
                  <FormGroupItem col={2} row={2}>
                    <FormikSelectInput
                      route="/accounts/majors/"
                      fieldName="student.major"
                    />
                  </FormGroupItem>
                  <FormGroupItem col={1} row={3}>
                    <Text weight="400">Grad Year</Text>
                  </FormGroupItem>
                  <FormGroupItem col={2} row={3}>
                    <FormikInput
                      fieldName="student.graduation_year"
                      type="text"
                    />
                  </FormGroupItem>
                </FormGroupGrid>
                <Button margin="1.5rem 0 0 0">
                  Save
                </Button>
              </Form >
            </Formik>
          </div>
        </CenterContainer>
      </MainContainer>
    </RootContainer >
  );
};
export default Accounts;

// TODO: figure out a resend verification code flow
// TODO: toasts
// TODO: add contact flow
// TODO: delete contact modal/confirmation
// TODO: make primary button
