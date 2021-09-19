import { Form, Formik } from "formik";
import { Heading } from "react-bulma-components";
import { useToasts } from "react-toast-notifications";
import { useResource } from "@pennlabs/rest-hooks";
import * as Yup from "yup";
import {
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
import ContactInput from "./Forms/ContactInput";
import { FormikSelectInput } from "./Forms/SelectInput";
import { ContactType, User } from "../../types";

const selectFields = (form: User) => ({
    first_name: form.first_name,
    student: form.student,
});

const FormSchema = Yup.object({
    first_name: Yup.string().required("Required"),
    student: Yup.object({
        graduation_year: Yup.number().required().positive().integer(),
    }),
});

const Accounts = ({ user: initialUser }: { user: User }) => {
    const { addToast } = useToasts();
    const { data: userPartial, mutate } = useResource<User>("/accounts/me/", {
        initialData: initialUser,
    });
    const user = userPartial!;

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
                        <Heading>{`Welcome, ${user.first_name}`}</Heading>
                        <Formik
                            initialValues={user}
                            validationSchema={FormSchema}
                            onSubmit={async (values, actions) => {
                                await mutate(selectFields(values));
                                addToast("Success!");
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
                                    <FormGroupItem
                                        col={1}
                                        row={1}
                                        alignItems="start"
                                    >
                                        <Text weight="400" marginTop="0.5rem">
                                            Email
                                        </Text>
                                    </FormGroupItem>
                                    <FormGroupItem
                                        col={2}
                                        row={1}
                                        alignItems="start"
                                    >
                                        <Flex
                                            flexDirection="column"
                                            alignItems="start"
                                            childMargin="0.2rem"
                                            width="100%"
                                        >
                                            <ContactInput
                                                route="/accounts/me/email/"
                                                initialData={user.emails}
                                                addText="Add another email address"
                                                contactType={ContactType.Email}
                                            />
                                        </Flex>
                                    </FormGroupItem>
                                    <FormGroupItem
                                        col={1}
                                        row={2}
                                        alignItems="start"
                                    >
                                        <Text weight="400" marginTop="0.5rem">
                                            Phone Number
                                        </Text>
                                    </FormGroupItem>
                                    <FormGroupItem
                                        col={2}
                                        row={2}
                                        alignItems="start"
                                    >
                                        <Flex
                                            flexDirection="column"
                                            alignItems="start"
                                            childMargin="0.2rem"
                                            width="100%"
                                        >
                                            <ContactInput
                                                route="/accounts/me/phonenumber/"
                                                initialData={user.phone_numbers}
                                                addText="Add a phone number"
                                                contactType={
                                                    ContactType.PhoneNumber
                                                }
                                            />
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
                                <Button margin="1.5rem 0 0 0">Save</Button>
                            </Form>
                        </Formik>
                    </div>
                </CenterContainer>
            </MainContainer>
        </RootContainer>
    );
};
export default Accounts;
