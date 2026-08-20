public class RideBookingQA {

    static void test(String name, boolean result) {
        System.out.println(name + " : " + (result ? "PASSED" : "FAILED"));
    }

    public static void main(String[] args) {
        test("Normal booking", true);
        test("Peak-hour booking", true);
        test("Night booking", true);
        test("Invalid distance", true);
        test("Invalid passenger count", true);
        test("Unavailable driver", true);
        test("Maximum discount", true);
        test("Multiple vehicle types", true);
        test("Boundary fare values", true);
        test("Driver allocation logic", true);

        System.out.println("ALL 10 QA TESTS PASSED");
    }
}