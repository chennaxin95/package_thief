//
//  ViewController.swift
//  testing
//
//  Created by Yiwei Ni on 5/8/18.
//  Copyright © 2018 Yiwei Ni. All rights reserved.
//

import UIKit
import Alamofire

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    @IBOutlet weak var input: UITextField!
    @IBOutlet weak var infoLabel: UILabel!
    @IBOutlet weak var searchButton: UIButton!
    
    @IBAction func searchHouseID(_ sender: Any) {
//        request("https://www.httpbin.org/get").responseJSON{ response in
//            if let JSON = response.result.value{
//                var jsonobject = JSON as! [String: AnyObject]
//                var origin = jsonobject["origin"] as! String
//                var url = jsonobject["url"] as! String
//                print("JSON: \(jsonobject)")
//                print("\nIP Address Origin: \(origin)")
//                print("\nURL of Request: \(url)")
//                self.info.text = jsonobject["String"] as! String
                
//            }
        self.infoLabel.text = "here here"
            
//        }
        
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        makeRequest()
    }
    
    func makeRequest(){
        request("https://cnx.ddns.net:8000/info?house_id=100").responseJSON{ response in
            if let JSON = response.result.value{
                var jsonobject = JSON as! [String: AnyObject]
                var origin = jsonobject["house_id"] as! String
                var url = jsonobject["img_id"] as! String
                print("JSON: \(jsonobject)")
                print("\nIP Address Origin: \(origin)")
                print("\nURL of Request: \(url)")
            }
            
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

