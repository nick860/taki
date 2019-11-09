using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        private Panel[,] cards = new Panel[2, 7];
        private Label[,] color = new Label[2, 7];
        private Label[,] sign = new Label[2, 7];
        private Label headline = new Label();
        private Label current = new Label();
        private Panel roaming = new Panel();
        private Label[] curcard = new Label[2];
        public Form1()
        {
            headline.Name = "headline";
            headline.Text = "Your cards";
            headline.Location = new Point(400, 20);
            headline.Size = new Size(300, 40);
            headline.Font = new Font("Comic Sans", 18);
            Controls.Add(headline);

            current.Name = "current card";
            current.Text = "Current card";
            current.Location = new Point(400, 330);
            current.Size = new Size(300, 40);
            current.Font = new Font("Comic Sans", 18);
            Controls.Add(current);

            roaming.Size = new Size(80, 100);
            roaming.BorderStyle = BorderStyle.FixedSingle;
            roaming.Location = new Point(400, 400);
            Name = "roaming";
            Controls.Add(roaming);

            for (int i = 0;i < 2; i++) ////////// I need to fix this
            {
                curcard[i] = new Label();
                if (i == 0)
                {
                    curcard[i].Name = "curcolor";
                    curcard[i].Text = "color: RED";
                    curcard[i].Location = new Point(5, 20);
                }
                else
                {
                    curcard[i].Name = "cursign";
                    curcard[i].Text = "69";
                    curcard[i].Location = new Point(25, 50);
                }
                roaming.Controls.Add(curcard[i]);
            }
            
            for (int i = 0; i < 2; i++)
                for (int j = 0; j < 7; j++)
                {
                    cards[i, j] = new Panel
                    {
                        Size = new Size(80, 100),
                        BorderStyle = BorderStyle.FixedSingle,
                        Location = new Point(j * 120 + 50, i * 120 + 70),
                        Name = i + "" + j
                    };
                    Controls.Add(cards[i, j]);

                    color[i,j] = new Label
                    {
                        Name = "color " + i + "" + j,
                        Text = "color: RED",
                        Location = new Point(5, 20)
                        
                    };
                    cards[i, j].Controls.Add(color[i, j]);

                    sign[i, j] = new Label
                    {
                        Name = "sign " + i + "" + j,
                        Text = "69",
                        Location = new Point(25, 50)
                    };
                    cards[i, j].Controls.Add(sign[i, j]);
                }
            InitializeComponent();
        }
    }
}
