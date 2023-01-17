import os
import cv2
import argparse


def main(srcPath: str, dstPath: str):

    p1 = None
    p2 = None
    frame = None
    frameTmp = None
    fileCount = 0

    def drawRectangle(event, x, y, flags, param):
        nonlocal p1, p2, frame, frameTmp
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"Clicked at {x} {y}")
            if p2:
                p1 = None
                p2 = None
                frameTmp = frame.copy()
            if not p1:
                p1 = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE:
            if p1 and not p2:
                frameTmp = frame.copy()
                cv2.rectangle(frameTmp, p1, (x, y), (0, 255, 0), 2)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            p2 = (x, y)
            cv2.rectangle(frameTmp, p1, p2, (0, 255, 0), 2)

    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", drawRectangle)

    for file in sorted(os.listdir(srcPath)):
        filePath = os.path.join(srcPath, file)
        if os.path.isfile(filePath):
            print(f"Opening {file}")
            frame = cv2.imread(filePath)
            if frame is None:
                continue
            frameTmp = frame.copy()

            while True:
                cv2.imshow("frame", frameTmp)
                k = cv2.waitKey(10)

                if k > 0:
                    print(k)

                match k:
                    case 27:
                        print("Pressed ESC...abort")
                        return
                    case 32:
                        print("Pressed SPACE...next image")
                        break
                    case 115: # s
                        dstFilePath = os.path.join(dstPath, f'{file}_{fileCount:05d}.jpg')
                        print(f"Save crop to {dstFilePath}")
                        minX = min(p1[0], p2[0])
                        maxX = max(p1[0], p2[0])
                        minY = min(p1[1], p2[1])
                        maxY = max(p1[1], p2[1])
                        cv2.imwrite(dstFilePath, frame[minY:maxY,
                                                       minX:maxX])
                        p1 = p2 = None
                        frameTmp = frame.copy()
                        fileCount += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='cropPages',
        description='Crops pages')
    parser.add_argument("src", default="src")
    parser.add_argument("dst", default="dst")
    args = parser.parse_args()
    print("Press 's' to save cropped area, SPACE to jump to next image and ESC to quit.")
    print(f"Source directory: {args.src}; Destination directory: {args.dst}")
    main(args.src, args.dst)
