import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { Button } from "@/components/ui/Button";

describe("Button", () => {
  test("renders button with text", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText("Click me")).toBeInTheDocument();
  });

  test("renders button with different variants", () => {
    const { container } = render(
      <>
        <Button variant="primary">Primary</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="accent">Accent</Button>
        <Button variant="outline">Outline</Button>
      </>
    );
    
    // Check for button elements
    const buttons = container.querySelectorAll("button");
    expect(buttons).toHaveLength(4);
  });

  test("renders button with different sizes", () => {
    const { container } = render(
      <>
        <Button size="sm">Small</Button>
        <Button size="md">Medium</Button>
        <Button size="lg">Large</Button>
      </>
    );
    
    const buttons = container.querySelectorAll("button");
    expect(buttons).toHaveLength(3);
  });

  test("calls onClick handler when clicked", () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText("Click me"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test("renders disabled button", () => {
    render(<Button disabled>Disabled</Button>);
    expect(screen.getByText("Disabled")).toBeDisabled();
  });

  test("renders button with custom className", () => {
    const { container } = render(
      <Button className="custom-button">Custom</Button>
    );
    
    expect(container.firstChild).toHaveClass("custom-button");
  });
});