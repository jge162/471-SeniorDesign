# Loop over frames from the camera
while True:
    # Capture the current frame from the camera
    ret, frame = cap.read()

    # Convert the frame to RGB format and resize it
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    size = common.input_size(interpreter)
    rgb = cv2.resize(rgb, size)

    # Pass the resized frame to the interpreter
    common.set_input(interpreter, rgb)

    # Run an inference
    interpreter.invoke()
    classes = classify.get_classes(interpreter, top_k=1)

    # Check if any class has a confidence score above 0.5
    any_conf_above_05 = False
    for c in classes:
        confidence = c.score
        if confidence > 0.5:
            any_conf_above_05 = True
            break

    # Print the result and check the class label and confidence score
    labels = dataset.read_label_file(label_file)
    if any_conf_above_05:
        for c in classes:
            class_label = labels.get(c.id, c.id)
            confidence = c.score
            if class_label == 'Recycling' and confidence > 0.5:
                pass
            elif class_label == 'Waste' and confidence > 0.5:
                pass
            elif class_label == 'Compost' and confidence > 0.5:
                pass
            print('%s %.5f' % (class_label, confidence))
    else:
        print("base case")

    # Display the frame with the confidence value
    cv2.putText(frame, "Confidence: %.2f" % confidence, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Object Detection', frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
