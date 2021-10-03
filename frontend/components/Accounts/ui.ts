import styled from "styled-components";

interface FlexProps {
    margin?: string;
    childMargin?: string;
    flexDirection?: string;
    alignItems?: string;
    justifyContent?: string;
    width?: string;
    position?: string;
}

export const Flex = styled.div<FlexProps>`
    display: flex;
    flex-direction: ${(props) =>
        props.flexDirection ? props.flexDirection : "row"};
    align-items: ${(props) => (props.alignItems ? props.alignItems : "center")};
    justify-content: ${(props) =>
        props.justifyContent ? props.justifyContent : "center"};
    margin: ${(props) => props.margin};
    width: ${(props) => props.width};
    position: ${(props) => props.position};

    & > * {
        margin: ${(props) => props.childMargin};
    }
`;

export const Span = styled.div<{ position?: string }>`
    position: ${(props) => props.position};
`;

export const RootContainer = styled.div`
    display: flex;
    flex-flow: column;
    height: 100%;
    background: #f7fbff;
`;

export const Nav = styled.div`
    background: #fefefe;
    box-shadow: 0px 2px 10px rgba(185, 185, 185, 0.32);
    z-index: 99;
    position: relative;
    display: flex;
    align-items: center;
    width: 100%;
    margin-bottom: 2rem;
`;

export const MainContainer = styled.div`
    flex: 1 1 auto;
    position: relative;
    overflow: auto;
    display: flex;
    justify-content: center;
    align-items: center;
`;

export const CenterContainer = styled.div`
    width: 50%;
    height: 85%;

    @media screen and (max-width: 800px) {
        width: 70%;
        height: 85%;
    }
`;

export const Logo = styled.img`
    width: 1.2rem;
    height: 1.2rem;
`;

export const Break = styled.hr`
    border: 1px solid #d3d3d3;
    background-color: #d3d3d3;
`;

interface TextProps {
    weight: string;
    size?: string;
    marginTop?: string;
}

export const Text = styled.span<TextProps>`
    font-weight: ${(props) => props.weight};
    font-size: ${(props) => (props.size ? props.size : "1rem")};
    margin-top: ${(props) => props.marginTop};
    white-space: nowrap;
`;

export const FormGroupHeader = styled.h3`
    font-style: normal;
    font-weight: 600;
`;

export const FormGroupGrid = styled.div`
    display: grid;
    grid-template-columns: 4fr 8fr;
    grid-auto-rows: minmax(3rem, auto);
`;

interface FormGroupItemProps {
    col: number;
    row: number;
    alignItems?: string;
}

export const FormGroupItem = styled.div<FormGroupItemProps>`
    grid-column: ${(props) => props.col};
    grid-row: ${(props) => props.row};
    display: flex;
    align-items: ${(props) => (props.alignItems ? props.alignItems : "center")};
`;

export const FormInput = styled.input<{ height?: string; error?: boolean }>`
    height: ${(props) => (props.height ? props.height : "2.3rem")};
    width: ${(props) => (props.width ? props.width : "100%")};
    outline: none;
    border: solid 1px #d6d6d6;
    border-radius: 0.2rem 0.2rem 0.2rem 0.2rem;
    border-color: ${(props) => (props.error ? "#e0b4b4" : "#d6d6d6")};
    background-color: ${(props) => props.error && "#fff6f6"};
    padding-left: 0.3rem;
`;

export const Indicator = styled.img<{ paddingTop?: string }>`
    width: 1rem;
    padding-top: ${(props) => props.paddingTop};
    cursor: pointer;
`;

export const Tag = styled.div`
    height: 1rem;
    margin-top: 0.35rem;
    background-color: #e7e7e7;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0.1rem;

    & > * {
        margin: 0.2rem;
        font-size: 0.5rem;
        font-weight: 600;
        color: #767676;
    }
`;

export const AddButton = styled.button<{ marginTop?: string }>`
    background: none !important;
    padding: 0 !important;
    border: none;
    cursor: pointer;
    color: #209cee;
    font-size: 1rem;
    font-weight: 500;
    margin-top: ${(props) => props.marginTop};
`;

export const Button = styled.button<{ margin?: string }>`
    background-color: #209cee;
    color: #ffffff;
    border: none;
    border-radius: 0.2rem;
    cursor: pointer;
    font-weight: 600;
    padding: 0.5rem 0.7rem 0.5rem 0.7rem;
    margin: ${(props) => props.margin};
`;

export const selectStyles = {
    container: (base) => ({
        ...base,
        width: "100%",
        padding: "0.5rem 0 0.5rem 0",
    }),
};
