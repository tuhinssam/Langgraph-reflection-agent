from src.graph import reflection_app

png_data = reflection_app.get_graph().draw_mermaid_png()

if __name__ == "__main__":
    #Write a 3-sentence summary of the India's unmanned landing in moon.
    user_prompt = input("Enter the prompt you wish to revise: ")
    result = reflection_app.invoke({"user_prompt": user_prompt})
    print("Final Output:", result["final"])
    print("Feedback:", result["feedback"])
    print("Total Iterations:", result["count"])


    # Specify the output filepath
    out_file = "output/graph.png"

    # Write to disk
    with open(out_file, "wb") as f:
        f.write(png_data)
        print(f"Saved graph image to {out_file}")

