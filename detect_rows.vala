using Gee;
using GLib.Math;

class Coords2D {
    public int x;
    public int y;
}

class LineRange {
    public int y0;
    public int y1; // non-inclusive
    
    public string to_string() {
        return y0.to_string()+"-"+y1.to_string();
    }
}

class BufChainElement {
    public uint8[] buffer;
}

class ImageObject {
    public Coords2D size;
    public uint8[] data; //raster grayscale data
}

class RowDetector : GLib.Object {
    public static Coords2D get_image_size(Gee.List<BufChainElement> input) throws GLib.SpawnError {
        var cmdline = new string[] {"gm", "identify", "-", "-format", "%w %h"};
        Pid pid;
        int stdin_handle;
        int stdout_handle;
        stdout.printf("qqq\n");
        GLib.Process.spawn_async_with_pipes (null, cmdline, null, SpawnFlags.SEARCH_PATH, null, out pid, out stdin_handle, out stdout_handle);
        var stdin_stream = FileStream.fdopen(stdin_handle, "wb");
        var stdout_stream = FileStream.fdopen(stdout_handle, "rb");
        stdout.printf("rrr\n");
        foreach (var bce in input) {
            stdin_stream.write(bce.buffer);
        }
        stdin_stream.flush();
        stdin_stream = null;
        stdout.printf("ggg\n");
//~         uint8[] output = new uint8[65536];
//~         var read_bytes = stdout_stream.read(output);
//~         stdout.printf("ttt%d\n", (int)read_bytes);
        string output = stdout_stream.read_line();
        var pieces = output.split(" ");
//~         var pieces = new string[2];
        GLib.Process.close_pid(pid);
        return new Coords2D() { x = pieces[0].to_int(), y = pieces[1].to_int() };
    }

    public static ImageObject load_image(Gee.List<BufChainElement> input) throws GLib.SpawnError {
        var size = get_image_size(input);
        stdout.printf("SIZE %d %d\n", size.x, size.y);
        var data = new uint8[size.x*size.y];
        var cmdline = new string[] {"gm", "convert", "-", "-monochrome", "-normalize", "GRAY:-"};
        Pid pid;
        int stdin_handle;
        int stdout_handle;
        GLib.Process.spawn_async_with_pipes (null, cmdline, null, SpawnFlags.SEARCH_PATH, null, out pid, out stdin_handle, out stdout_handle);
        var stdin_stream = FileStream.fdopen(stdin_handle, "wb");
//~         var stdin_stream = FileStream.open("ttt.jpg", "wb");
        var stdout_stream = FileStream.fdopen(stdout_handle, "rb");
        foreach (var bce in input) {
            stdin_stream.write(bce.buffer);
        }
        stdin_stream.flush();
        stdin_stream = null;
        var read_bytes = stdout_stream.read(data);
        stdout.printf("RBYTES %d\n", (int)read_bytes);
        assert(read_bytes==size.x*size.y);
        GLib.Process.close_pid(pid);
        return new ImageObject() { size=size, data=data };
    }

    public static double[] get_sq_dev_per_line(ImageObject image, uint8 target_color) throws Error {
        var res = new double[image.size.y];
        for (var y = 0; y<image.size.y; y++) {
            // quadratic deviation
            double sq_dev = 0;
            for (var x = 0; x<image.size.x; x++) {
                var point = image.data[image.size.x*y+x];
                sq_dev += (target_color-point) * (target_color-point);
            }
            res[y] = sq_dev;
        }
        return res;
    }
    
    public static Gee.List<bool> get_filled_lines(ImageObject image, uint8 target_color) throws Error {
        var res = new ArrayList<bool>();
        var sq_devs = get_sq_dev_per_line(image, 255);
        var thresh = 1.0*image.size.x*(20*20);
        for (int y = 0; y<image.size.y; y++) {
            res.add(sq_devs[y]>thresh);
        }
        return res;
    }

    public static Gee.List<LineRange> get_ranges(Gee.List<BufChainElement> input, uint8 target_color, double min_row_ratio) throws Error {
        var image = load_image(input);

        var filled_lines = get_filled_lines(image, target_color);
            stdout.printf("gotranges\n");
        var res = new ArrayList<LineRange>();
        
        var start = -1;
        var min_row_pixels = (int)Math.floor(image.size.y*min_row_ratio);
        for (int y = 0; y<=image.size.y; y++) {
            var filled = (y<image.size.y) && filled_lines[y];
            if (filled) {
                if (start==-1) {
                    start = y;
                }
            }
            else {
                if (start!=-1) {
                    if (y-start>min_row_pixels) {
                        res.add(new LineRange() { y0=start, y1=y });
                        start = -1;
                    }
                }
            }
        }
        return res;
    }

    public static int main(string[] args) {
        try {
            var buf_list = new ArrayList<BufChainElement>();
            size_t read_bytes;
            while (true) {
                var buf = new uint8[65536];
                read_bytes = stdin.read(buf);
                if (read_bytes>0) {
                    stdout.printf("zzz%d\n", (int)read_bytes);
                    buf.resize((int)(uint64)read_bytes);
                    var bce = new BufChainElement() {buffer=buf};
                    stdout.printf("zzy\n");
                    buf_list.add(bce);
                    stdout.printf("zzz\n");
                } else {
                    break;
                }
            }
            var rngs = get_ranges(buf_list, 255, 0.125);
            foreach (var r in rngs) {
                stdout.printf(r.to_string()+"\n");
            }
        }
        catch (Error e) {
            stderr.printf("ERROR: "+e.message+"\n");
            return 1;
        }
        return 0;
    }
}
 
