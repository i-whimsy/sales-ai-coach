import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { Input } from "@/components/ui/Input";

describe("Input", () => {
  test("renders input element", () => {
    render(<Input placeholder="Enter text" />);
    expect(screen.getByPlaceholderText("Enter text")).toBeInTheDocument();
  });

  test("renders different input types", () => {
    const { container } = render(
      <>
        <Input type="text" data-testid="text-input" />
        <Input type="password" data-testid="password-input" />
        <Input type="email" data-testid="email-input" />
        <Input type="number" data-testid="number-input" />
      </>
    );
    
    const inputs = container.querySelectorAll("input");
    expect(inputs).toHaveLength(4);
    expect(container.querySelector('[data-testid="text-input"]')).toHaveAttribute("type", "text");
    expect(container.querySelector('[data-testid="password-input"]')).toHaveAttribute("type", "password");
    expect(container.querySelector('[data-testid="email-input"]')).toHaveAttribute("type", "email");
    expect(container.querySelector('[data-testid="number-input"]')).toHaveAttribute("type", "number");
  });

  test("handles change events", () => {
    const handleChange = jest.fn();
    render(<Input onChange={handleChange} />);
    
    fireEvent.change(screen.getByRole("textbox"), {
      target: { value: "test value" },
    });
    
    expect(handleChange).toHaveBeenCalledTimes(1);
  });

  test("displays entered value", () => {
    const { container } = render(<Input defaultValue="initial value" />);
    expect(container.querySelector("input")).toHaveValue("initial value");
  });

  test("renders with custom className", () => {
    const { container } = render(<Input className="custom-input" />);
    expect(container.firstChild).toHaveClass("custom-input");
  });

  test("renders disabled input", () => {
    render(<Input disabled />);
    expect(screen.getByRole("textbox")).toBeDisabled();
  });

  test("supports placeholder", () => {
    render(<Input placeholder="Enter your email" />);
    expect(screen.getByPlaceholderText("Enter your email")).toBeInTheDocument();
  });
});